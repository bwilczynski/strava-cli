import nox

nox.options.sessions = ["lint"]

locations = "sonos", "noxfile.py"


@nox.session
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-black")
    session.run("flake8", *args)


@nox.session
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
