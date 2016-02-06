{pkgs, pythonPackages, stdenv}:
let
    pp = pythonPackages;
in
with pp;
pythonPackages //
rec {
    pysdl2 = buildPythonPackage {
        name = "pysdl2-0.9.3";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/P/PySDL2/PySDL2-0.9.3.zip;
            md5 = "0e3b1efa5f534666e8750b28915237ed";
        };
        buildInputs = [pkgs.SDL2];
    };

    wiringpi = buildPythonPackage {
        name = "wiringpi";
        src = pkgs.fetchurl {
            url = https://github.com/WiringPi/WiringPi2-Python/archive/4ad103ca49de3b05f2c749e7445ece35c5e6b390.tar.gz;
            sha256 = "13qcrwibv33cm2cky7almqai1li853njirz0qmlbwa3l764dr6qg";
        };
    };

    pygments = buildPythonPackage {
        name = "pygments";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/P/Pygments/Pygments-2.0.2.tar.gz;
            md5 = "238587a1370d62405edabd0794b3ec4a";
        };
    };

    prompt_toolkit = buildPythonPackage {
        name = "prompt-toolkit";
        propagatedBuildInputs = [ six wcwidth pygments ];
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/p/prompt_toolkit/prompt_toolkit-0.57.tar.gz;
            md5 = "280284f7ecf5454143f90c3ec8b0750d";
        };
    };

    jedi = buildPythonPackage {
        name = "jedi";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/j/jedi/jedi-0.9.0.tar.gz;
            md5 = "2fee93d273622527ef8c97ac736e92bd";
        };
    };

    ptpython = buildPythonPackage {
        name = "ptpython";
        propagatedBuildInputs = [ wcwidth six prompt_toolkit docopt jedi pygments];
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/p/ptpython/ptpython-0.28.tar.gz;
            md5 = "f563f435185d5681f754310c96fe9cfe";
        };
    };

    six = buildPythonPackage {
        name = "six";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz;
            md5 = "34eed507548117b2ab523ab14b2f8b55";
        };
    };

    rpigpio = buildPythonPackage {
        name = "rpi.gpio";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.6.1.tar.gz;
            md5 = "254d0443a436eb241367c487274e7197";
        };
    };

    protobuf = buildPythonPackage {
        name = "protobuf";
        propagatedBuildInputs = [ six ];
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/p/protobuf/protobuf-3.0.0b2.tar.gz;
            md5 = "f0d3bd2394345a9af4a277cd0302ae83";
        };
    };

    setproctitle = buildPythonPackage {
        name = "setproctitle";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/s/setproctitle/setproctitle-1.1.9.tar.gz;
            md5 = "95d9e56c69437246460a20804961d70d";
        };
    };

    websockets = buildPythonPackage {
        name = "websockets-3.0";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/w/websockets/websockets-3.0.tar.gz;
            md5 = "6575c706f010a5a52a449b3c2dbba84d";
        };
    };
}
