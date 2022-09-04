import click

@click.group(name="user")
def user():
    pass

@user.command("add", help="Add a user.")
def add_user():
    pass

if __name__ == "__main__":
    user()