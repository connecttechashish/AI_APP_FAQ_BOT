import json
import os
import urllib.request

from .prompts import SYSTEM_PROMPT
from .tools import retrieve_faq


class FAQAgent:
    def __init__(
        self,
        k=3,
        threshold=0.3,
        use_ollama=False,
        ollama_host=None,
        ollama_model=None,
    ):
        self.k = k
        self.threshold = threshold
        self.history = []
        self.use_ollama = use_ollama
        self.ollama_host = ollama_host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.ollama_model = ollama_model or os.getenv("OLLAMA_MODEL", "llama3.1")

    def _build_sources(self, results):
        sources = []
        for idx, item in enumerate(results, start=1):
            sources.append(f"[{idx}] {item['question']}")
        return sources

    def _fallback_answer(self, results):
        if not results:
            return "I could not find an answer. Can you rephrase the question?"
        top = results[0]
        answer = f"{top['answer']}\n\nSources:\n{self._format_sources(results)}"
        return answer

    def _format_sources(self, results):
        lines = []
        for idx, item in enumerate(results, start=1):
            lines.append(f"[{idx}] {item['question']}")
        return "\n".join(lines)

    def _ollama_generate(self, prompt):
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
        }
        req = urllib.request.Request(
            f"{self.ollama_host}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("response", "").strip()

    def _build_prompt(self, query, results):
        sources = []
        for idx, item in enumerate(results, start=1):
            sources.append(
                f"[{idx}] Q: {item['question']}\nA: {item['answer']}"
            )

        history_lines = []
        for turn in self.history[-6:]:
            history_lines.append(f"{turn['role']}: {turn['content']}")

        parts = [
            SYSTEM_PROMPT,
            "Conversation history:",
            "\n".join(history_lines) or "(none)",
            "Sources:",
            "\n\n".join(sources),
            f"User question: {query}",
        ]
        return "\n\n".join(parts)

    def chat(self, query):
        results, low_confidence = retrieve_faq(
            query, k=self.k, threshold=self.threshold
        )
        self.history.append({"role": "user", "content": query})

        if low_confidence:
            response = "I am not sure I have the right match. Which FAQ section is this related to?"
            self.history.append({"role": "assistant", "content": response})
            return response

        if self.use_ollama:
            try:
                prompt = self._build_prompt(query, results)
                response = self._ollama_generate(prompt)
            except Exception:
                response = self._fallback_answer(results)
        else:
            response = self._fallback_answer(results)

        if "Sources:" not in response:
            response = f"{response}\n\nSources:\n{self._format_sources(results)}"

        self.history.append({"role": "assistant", "content": response})
        return response
