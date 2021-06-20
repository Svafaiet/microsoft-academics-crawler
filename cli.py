import os
from pathlib import Path

import numpy as np
import typer
import typing

from config import config
from hits import Hits
from microsoftaca.extractor_process import extractor_process
from papergraph import PaperGraph

cli = typer.Typer(
    name="microaca",
    no_args_is_help=True,
    add_help_option=True,
    help="""
        cli for microsoft academy crawl and recommender systems
        Use crawl              to start the crawl
        
        Use pagerank           to generate pagerank
        
        Use hits               to find best authorities
        
        Use suggest-paper      to suggest papers similar to a user profile
        
        Use suggest-profile    to get normalized user profile with other user profile suggestions
        
        Use recover            to recover matrix which is sparse
    """
)


@cli.command("crawl")
def crawl(
    output: typing.Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Where to write CrawledPapers.json",
        atomic=True,
        is_eager=True,
    ),
):
    """
        Starts crawling https://academic.microsoft.com/

        Use Ctrl+C once to stop gracefully, if you interrupt twice cache will be broken
        and you need to use delete-cache command.

        Use this command again to resume crawl after a graceful stop.
    """
    extractor_process(json_file_out=output)


@cli.command("delete-cache")
def delete_cache():
    """
        Deletes cache, Use this to restart crawl.
    """
    try:
        os.rmdir(config.STATE_PATH)
    except OSError as e:
        typer.echo("Could not remove states, Error: %s : %s" % (config.STATE_PATH, e.strerror))

    jl_path = os.path.join(config.PAPER_PATH, "papers.jl")
    try:
        os.remove(jl_path)
    except OSError as e:
        typer.echo("Could not remove papers, Error: %s : %s" % (str(jl_path), e.strerror))


@cli.command("pagerank")
def pagerank(
    inputf: typing.Optional[Path] = typer.Option(
        None,
        "--input",
        "-i",
        help="path to read CrawledPapers.json or jl file",
        atomic=True,
        is_eager=True,
    ),
    output: typing.Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="directory to write PageRank.json",
        atomic=True,
        is_eager=True,
    ),
):
    """
        Use pagerank -i "<path-to-json-dir>/CrawledPapers.json" -o "<dir>"

        Page rank json will be written in <dir>/PageRank.json
    """
    pg = PaperGraph()
    pg.load_graph(filename=inputf)
    pr = pg.get_pagerank()
    typer.echo("Page rank is {}".format(str(pr)))
    pg.output(pr, filepath=output)
    typer.echo("Written to {}".format(((str(output) + "/") if output else "") + "PageRank.json"))


@cli.command("hits")
def hits(
    inputf: typing.Optional[Path] = typer.Option(
        None,
        "--input",
        "-i",
        help="path to read CrawledPapers.json or jl file",
        atomic=True,
        is_eager=True,
    ),
    n: int = typer.Option(
        5,
        "-n",
        help="Number of best authorities to show",
    ),
):
    """
        Use

        hits -n 7 -i "<path-to-json-dir>/CrawledPapers.json"

        prints top n authorities based on input file
    """
    h = Hits()
    h.load_graph(filename=inputf)
    typer.echo("Top {} authors: {}".format(n, h.get_top_authors(n)))


if __name__ == '__main__':
    cli()
