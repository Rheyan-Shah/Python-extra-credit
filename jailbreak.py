"""Jailbreak: a tiny text game. Escape the prison cell!"""

def ask(prompt, options):
    while True:
        a = input(f"{prompt} ({'/'.join(options)}): ").strip().lower()
        if a in options:
            return a
        print("Pick one of the options.")

def main():
    print("You wake up in a prison cell. Time to break out!")
    has_spoon = False
    has_key = False

    if ask("Check the 'bed' or the 'wall'?", ["bed", "wall"]) == "bed":
        print("You find a spoon under the mattress.")
        has_spoon = True
    else:
        print("The wall is solid. You lose time.")

    if ask("Dig the 'floor' or pick the 'lock'?", ["floor", "lock"]) == "floor":
        if has_spoon:
            print("You dig through the floor with the spoon into a tunnel!")
        else:
            print("No tool! A guard hears you scratching. Busted.")
            return
    else:
        print("You can't pick it with bare hands. Busted.")
        return

    print("In the tunnel you find a guard's key ring.")
    has_key = True

    if ask("Exit via the 'gate' or the 'fence'?", ["gate", "fence"]) == "gate" and has_key:
        print("The key opens the gate. YOU ESCAPED! 🎉")
    else:
        print("The fence is electrified. Busted.")

if __name__ == "__main__":
    main()
