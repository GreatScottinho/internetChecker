import InternetChecker
import time

def log_connection_status():
    pass

def main():

    # Create internetChecker
    checker = InternetChecker.InternetChecker()

    # Check status
    status = checker.get_connection_status()
    print(status)

    # Log connection status
    log_connection_status()

    # Both good
    if (status["dsl"] == "CONNECTED" and status["internet"] == "CONNECTED"):
        print("Internet's good!")
        return

    else:
        print("Something is wrong... trying to connect.")
        checker.connect()

    time.sleep(45)
    checker.tear_down()

    # # DSL down
    # elif (status["dsl"] != "CONNECTED" and status["internet"] == "CONNECTED"):
    #     pass

    # # Internet down
    # elif (status["dsl"] == "CONNECTED" and status["internet"] != "CONNECTED"):
    #     pass

    # # Default (both down)
    # else:
    #     pass



if __name__ == "__main__":
    main()