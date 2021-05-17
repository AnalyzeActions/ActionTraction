import typer

app = typer.Typer()

@app.callback()
def callback():
    """ Action Traction"""

@app.command()
def import_repo():
    """ Import GitHub repository credentials"""
    typer.echo("GitHub repository credentials")

@app.command()
def determine_metrics():
    """Determine user specified metrics to run"""
    typer.echo("Determining metrics to run")

