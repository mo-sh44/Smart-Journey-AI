import json
import os
import sys
import time

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import openai
from dotenv import load_dotenv

from core.tool_dispatcher import ToolDispatcher

load_dotenv(override=True)

_WAITING = {"queued", "in_progress", "cancelling"}
_TERMINAL = {"completed", "failed", "expired", "cancelled"}


class OpenAIHandler:
    def __init__(self):
        self._client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._assistant_id = os.getenv("ASSISTANT_ID")
        self._thread_id = self._client.beta.threads.create().id
        self._dispatcher = ToolDispatcher()

    def send_message(self, user_input: str) -> str:
        self._clear_active_runs()
        self._client.beta.threads.messages.create(
            thread_id=self._thread_id, role="user", content=user_input
        )
        run = self._client.beta.threads.runs.create(
            thread_id=self._thread_id, assistant_id=self._assistant_id
        )
        self._wait_for_run(run.id)
        return self._get_latest_response()

    def _clear_active_runs(self) -> None:
        try:
            runs = self._client.beta.threads.runs.list(thread_id=self._thread_id, limit=5)
        except Exception:
            return

        for run in runs.data:
            if run.status in _WAITING or run.status == "requires_action":
                started_at = time.time()
                while time.time() - started_at < 10:
                    current = self._client.beta.threads.runs.retrieve(
                        thread_id=self._thread_id, run_id=run.id
                    )
                    if current.status in _TERMINAL:
                        break
                    time.sleep(0.8)
                else:
                    try:
                        self._client.beta.threads.runs.cancel(
                            thread_id=self._thread_id, run_id=run.id
                        )
                    except Exception:
                        pass

    def _wait_for_run(self, run_id: str) -> None:
        started_at = time.time()
        while True:
            if time.time() - started_at > 120:
                raise TimeoutError("Assistant run took too long. Please try again.")

            run = self._client.beta.threads.runs.retrieve(
                thread_id=self._thread_id, run_id=run_id
            )
            status = run.status
            if status == "completed":
                break
            if status == "failed":
                last_error = getattr(run, "last_error", None)
                message = last_error.message if last_error else "No error details returned by OpenAI."
                raise RuntimeError(message)
            if status in {"expired", "cancelled"}:
                raise RuntimeError(f"Assistant run ended with status: {status}")
            if status == "requires_action":
                self._handle_tool_calls(run_id, run)
            else:
                time.sleep(0.8)

    def _handle_tool_calls(self, run_id: str, run) -> None:
        pending_calls = run.required_action.submit_tool_outputs.tool_calls
        outputs = []
        for call in pending_calls:
            fn_name = call.function.name
            fn_args = json.loads(call.function.arguments)
            print(f"Tool call: {fn_name}({fn_args})".encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
            result = self._dispatcher.dispatch(fn_name, fn_args)
            preview = str(result).replace("\n", " ")[:500]
            print(f"Tool result: {preview}".encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
            outputs.append({"tool_call_id": call.id, "output": str(result)})
        self._client.beta.threads.runs.submit_tool_outputs(
            thread_id=self._thread_id, run_id=run_id, tool_outputs=outputs
        )

    def _get_latest_response(self) -> str:
        messages = self._client.beta.threads.messages.list(thread_id=self._thread_id)
        return messages.data[0].content[0].text.value
