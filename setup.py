import sys,os,site,shutil,subprocess,shlex
from setuptools import setup,Extension

try:
    os.chdir(os.path.split(__file__)[0])
    sys.path.append(os.getcwd())
except Exception:pass
sys.path.extend(site.getsitepackages()+[site.getusersitepackages()])
import no_subclasses

if "sdist" in sys.argv[1:]:
    if not os.path.isfile("README.rst") or \
       (os.stat("README.md").st_mtime > os.stat("README.rst").st_mtime):
        if shutil.which("pandoc"):
            cmd="pandoc -t rst -o README.rst README.md"
            print("Running pandoc:",cmd,"...")
            result=subprocess.run(shlex.split(cmd))
            print("Return code:",result.returncode)
        else:
            print("Pandoc command for generating README.rst is required",
                  file=sys.stderr)
            sys.exit(1)
    long_desc=open("README.rst",encoding="utf-8").read()
else:
    long_desc=""

setup(
    name='no-subclasses',
    version=no_subclasses.__version__,
    description=no_subclasses.__doc__.replace("\n"," "),
    long_description=long_desc,
    author="ekcbw",
    author_email="u81430728@163.com",
    url="https://github.com/ekcbw/no-subclasses",
    packages=['no_subclasses'],
    keywords=["subclasses","exec","eval","sandbox","security",
              "environment"],
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=["pyobject","pydetour"],
)
