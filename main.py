import InternetChecker


def main():

    # Create internetChecker
    checker = InternetChecker.InternetChecker(headless=False)

    # Check status
    try:
        status = checker.get_connection_status()

        # Both good
        if (status["dsl"] == "CONNECTED" and status["internet"] == "CONNECTED"):
            print("Internet's good!")

        else:
            print("Something is wrong... trying to connect.")
            checker.connect()
        
    except Exception as e:
        print(e)

    checker.tear_down()


if __name__ == "__main__":
    main()