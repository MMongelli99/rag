import ollama
from ollama import Client, GenerateResponse
from datetime import timedelta

if __name__ == "__main__":
    client: Client = ollama.Client()

    model: str = "llama3.1"

    print(f'Welcome to the {model} chat client! Enter "q" at any time to quit.')

    try:
        while (prompt := input(f"{model} > ").strip()) != "q":
            try:
                res: GenerateResponse = client.generate(model=model, prompt=prompt)
                duration: int = int(
                    int(timedelta(seconds=seconds).total_seconds())
                    if (seconds := (res.eval_duration or 0) // 1_000_000_000)
                    else 0
                )
                took: str = f" (took {duration}s)" if duration > 0 else ""
                print(f"# {model}{took}")
                print(res.response)
            except Exception as e:
                print(e)
    except (EOFError, KeyboardInterrupt):
        pass

    print()
    print(f"Quitting {model} chat client.")
