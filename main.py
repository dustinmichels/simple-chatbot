from utils import print_face, prompter, robo_print
from helper import load_or_download, get_terms


def main():
    sents = load_or_download()
    end = ["quit", "goodbye", "exit", "leave", "thanks", "done"]

    print_face()
    response = prompter("Hey! Ask me about bacteria <:^")

    while response.lower() not in end:
        terms = get_terms(response)

        success = False
        for term in terms:
            found = [s for s in sents if term in s["tokenized"]]
            if found:
                robo_print(found[0]["sent"])
                success = True
                break
        if not success:
            robo_print("Great question! I don't know...")

        response = prompter("\nAnother question?")

    print("Goodbye!")


if __name__ == "__main__":
    main()
