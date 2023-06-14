#!/usr/bin/python3.8
 
def echo(text: str = "lalalalal", repetitions: int = 3) -> str:
    """Imitate a real-world echo."""
    echoed_text = ""
    print(text)
    for i in range(repetitions, 0, -1):
        echoed_text += f"{text[-i:]}\n"
    print(f"{echoed_text.lower()}.")
    return f"{echoed_text.lower()}."

if __name__ == "__main__":
    echo()
