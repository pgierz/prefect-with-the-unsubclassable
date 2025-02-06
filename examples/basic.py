from prefect import flow, task


@task
def say_hello():
    print("Hello, Prefect!")


@flow
def main():
    say_hello()


if __name__ == "__main__":
    main()
