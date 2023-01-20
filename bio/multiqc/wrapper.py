"""Snakemake wrapper for trimming paired-end reads using cutadapt."""

__author__ = "Julian de Ruiter"
__copyright__ = "Copyright 2017, Julian de Ruiter"
__email__ = "julianderuiter@gmail.com"
__license__ = "MIT"


from pathlib import Path
from tempfile import TemporaryDirectory

from snakemake.shell import shell


extra = snakemake.params.get("extra", "")
# Set this to False if multiqc should use the actual input directly
# instead of parsing the folders where the provided files are located
use_input_files_only = snakemake.params.get("use_input_files_only", False)

if not use_input_files_only:
    input_data = set(map(lambda x: Path(x).parent, snakemake.input))
else:
    input_data = set(map(Path, snakemake.input))

html_out = Path(snakemake.output.get("html", "./multiqc_results.html"))
datazip_out = Path(snakemake.output["zip"]) if snakemake.output.get("zip") else None

log = snakemake.log_fmt_shell(stdout=True, stderr=True)

with TemporaryDirectory() as tempdir:
    shell(
        "multiqc"
        " {extra}"
        " --force"
        " -o {tempdir:q}"
        " -n {html_out.name}"
        " --zip-data-dir"
        " {input_data}"
        " {log}"
    )

    tmp_html = Path(tempdir) / html_out.name
    tmp_zip = Path(tempdir).joinpath(html_out.stem + "_data.zip")

    if html_out != tmp_html:
        shell("mv {tmp_html:q} {html_out:q}")
    if datazip_out is not None and datazip_out != tmp_zip:
        shell("mv {tmp_zip:q} {datazip_out:q}")
