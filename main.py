import checker


def main():

    # Create checker
    internet_checker = checker.InternetChecker(headless=False)

    # Check status
    try:
        status = internet_checker.get_connection_status()

        # Both good
        if (status["dsl"] == "CONNECTED" and status["internet"] == "CONNECTED"):
            print("Internet's good!")

        else:
            print("Something is wrong... trying to connect.")
            internet_checker.connect()
        
    except Exception as e:
        print(e)

    internet_checker.tear_down()


if __name__ == "__main__":
    main()