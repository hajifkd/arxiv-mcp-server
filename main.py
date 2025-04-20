from mcp.server.fastmcp import FastMCP
import arxiv
import datetime
import tempfile
import tarfile

mcp = FastMCP("arXiv server")

@mcp.tool()
def download_arxiv_paper(paper_id: str) -> str:
    """
    Download an arXiv paper given its ID.
    ID should be in the format "XXXX.XXXXX", "XXXX.XXXX" or "category/XXXXXXX".
    """
    search = arxiv.Search(id_list=[paper_id])
    # Create a client instance
    paper = next(arxiv.Client().results(search))

    # Create a temporary directory to store the source files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download the source files
        paper.download_source(filename=f"{temp_dir}/source.tar.gz")
        # Extract the tarball
        with tarfile.open(f"{temp_dir}/source.tar.gz", "r:gz") as tar:
            tar.extractall(path=temp_dir)
            # Create a list of the extracted files
            extracted_files = []
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith(('.tex', '.bib')):
                    extracted_files.append(f"{temp_dir}/{member.name}")

        # combine all files into a single string
        combined_content = ""
        for file in extracted_files:
            with open(file, 'r') as f:
                combined_content += f.read() + "\n"
        # Return the combined content
        return combined_content


@mcp.tool()
def today_arxiv(category: str) -> list:
    """
    Get the latest arXiv papers in a given category.
    """
    today = datetime.date.today()
    today_str = today.strftime("%Y%m%d")
    # Fetch the latest papers from arXiv
    search = arxiv.Search(
        query=f"cat:{category} AND submittedDate:[{today_str}0000 TO {today_str}2359]",
        max_results=100,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    # Call the reusable function to fetch and process results
    return fetch_arxiv_results(search)

@mcp.tool()
def weekly_arxiv(category: str) -> list:
    """
    Get the latest arXiv papers in a given category for the past week.
    """
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    week_ago_str = week_ago.strftime("%Y%m%d")
    today_str = today.strftime("%Y%m%d")
    
    # Fetch the latest papers from arXiv
    search = arxiv.Search(
        query=f"cat:{category} AND submittedDate:[{week_ago_str}0000 TO {today_str}2359]",
        max_results=200,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    # Call the reusable function to fetch and process results
    return fetch_arxiv_results(search)

@mcp.tool()
def search_arxiv(query: str) -> list:
    """
    Search arXiv for papers matching a query.
    """
    # Fetch the latest papers from arXiv
    search = arxiv.Search(
        query=query,
        max_results=50,
        sort_by=arxiv.SortCriterion.Relevance
    )
    # Call the reusable function to fetch and process results
    return fetch_arxiv_results(search)

def fetch_arxiv_results(search):
    """
    Fetch and process arxiv search results into a structured format.
    
    Args:
        search: An arxiv.Search object configured with query parameters
        
    Returns:
        list: A list of dictionaries containing paper information
    """
    # Create a client instance
    client = arxiv.Client()
    
    # Collect the results 
    results = []
    for result in client.results(search):
        results.append({
            "title": result.title,
            "summary": result.summary,
            "published": result.published,
            "id": result.entry_id,
            "authors": [author.name for author in result.authors],
            "categories": result.categories,
        })

    return results

def main():
    # Run the server
    mcp.run()

if __name__ == "__main__":
    main()