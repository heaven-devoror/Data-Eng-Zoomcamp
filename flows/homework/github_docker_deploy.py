from prefect.filesystems import GitHub

github_block = GitHub(
    repository="https://github.com/heaven-devoror/Data-Eng-Zoomcamp",

)
github_block.get_directory("flows")
github_block.save("test")
