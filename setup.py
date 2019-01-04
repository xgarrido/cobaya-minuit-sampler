from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

def unlink_minuit_to_cobaya():
    import cobaya
    import os
    os.unlink(cobaya.__path__[0] + "/samplers/minuit")

def link_minuit_to_cobaya():
    import cobaya
    import minuit
    import os
    unlink_minuit_to_cobaya()
    os.symlink(minuit.__path__[0], cobaya.__path__[0] + "/samplers/minuit")

class PostDevelopCommand(develop):
    """Post-command for development mode."""
    def run(self):
        develop.run(self)
        link_minuit_to_cobaya()

class PostInstallCommand(install):
    """Post-command for installation mode."""
    def run(self):
        install.run(self)
        link_minuit_to_cobaya()

setup(name="cobaya-minuit-sampler",
      version = "0.1",
      packages = find_packages(),
      description = "Minuit sampler for cobaya",
      url = "https://github.com/thibautlouis/beyondCV",
      author = "Xavier Garrido",
      author_email = "xavier.garrido@lal.in2p3.fr",
      keywords = ["CMB", "minimization", "sampler", "minuit"],
      classifiers = ["Intended Audience :: Science/Research",
                     "Topic :: Scientific/Engineering :: Astronomy",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: 3.7"],
      install_requires = ["cobaya"],
      cmdclass={
          "develop": PostDevelopCommand,
          "install": PostInstallCommand,
      },
)
