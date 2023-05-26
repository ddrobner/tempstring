# pdoc errors otherwise
if __name__ == '__main__':
    import pdoc
    import os
    from pathlib import Path
    from globals import globalmanager
    from shutil import rmtree

    globalmanager.setParam({"debug": False})
    rmtree("docs")
    pdoc.render.configure(docformat='google')
    doc = pdoc.pdoc(Path(os.getcwd()), output_directory=Path(os.path.join(os.getcwd(), "docs")))
