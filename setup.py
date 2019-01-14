from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

def link_minuit_to_cobaya(develop_mode=True):
    if develop_mode:
        import minuit
        src = minuit.__path__[0]
        import cobaya
        dest = cobaya.__path__[0] + "/samplers/minuit"
    else:
        from distutils.sysconfig import get_python_lib
        src = get_python_lib() + "/minuit"
        dest = get_python_lib() + "/cobaya/samplers/minuit"
    import os
    if os.path.islink(dest):
        os.unlink(dest)
    os.symlink(src, dest)

class PostDevelopCommand(develop):
    """Post-command for development mode."""
    def run(self):
        develop.run(self)
        link_minuit_to_cobaya(develop_mode=True)

class PostInstallCommand(install):
    """Post-command for installation mode."""
    def run(self):
        install.run(self)
        link_minuit_to_cobaya(develop_mode=False)

setup(name="cobaya-minuit-sampler",
      version = "0.1",
      packages = find_packages(),
      description = "Minuit sampler for cobaya",
      url = "https://github.com/xgarrido/cobaya-minuit-sampler",
      author = "Xavier Garrido",
      author_email = "xavier.garrido@lal.in2p3.fr",
      keywords = ["CMB", "minimization", "sampler", "minuit"],
      classifiers = ["Intended Audience :: Science/Research",
                     "Topic :: Scientific/Engineering :: Astronomy",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: 3.7"],
      install_requires = ["cobaya", "iminuit"],
      package_data = {"minuit": ["*.yaml"]},
      cmdclass={
          "develop": PostDevelopCommand,
          "install": PostInstallCommand,
      }
)
