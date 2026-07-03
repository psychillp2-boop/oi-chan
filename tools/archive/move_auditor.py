from controller.move_controller import run_move_system

def main():
    print("=== EA_SYSTEM AUDITOR START ===")

    target = "C:\\Users\\PC\\Desktop\\EA_SYSTEM"

    run_move_system(target)


if __name__ == "__main__":
    main()