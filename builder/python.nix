{pythonPackages, pkgs}:
let
    pp = pythonPackages;
in pp // rec {

    pygments = pp.buildPythonPackage {
        name = "pygments";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/P/Pygments/Pygments-2.0.2.tar.gz;
            md5 = "238587a1370d62405edabd0794b3ec4a";
        };
    };

    prompt_toolkit = pp.buildPythonPackage {
        name = "prompt-toolkit";
        propagatedBuildInputs = [ six pp.wcwidth pygments ];
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/p/prompt_toolkit/prompt_toolkit-0.57.tar.gz;
            md5 = "280284f7ecf5454143f90c3ec8b0750d";
        };
    };

    jedi = pp.buildPythonPackage {
        name = "jedi";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/j/jedi/jedi-0.9.0.tar.gz;
            md5 = "2fee93d273622527ef8c97ac736e92bd";
        };
    };

    ptpython = pp.buildPythonPackage rec {
        name = "ptpython";
        propagatedBuildInputs = [ pp.wcwidth six prompt_toolkit pp.docopt jedi pygments];
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/p/ptpython/ptpython-0.28.tar.gz;
            md5 = "f563f435185d5681f754310c96fe9cfe";
        };
    };

    six = pp.buildPythonPackage {
        name = "six";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz;
            md5 = "34eed507548117b2ab523ab14b2f8b55";
        };
    };

    rpigpio = pp.buildPythonPackage {
        name = "rpi.gpio";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.6.1.tar.gz;
            md5 = "254d0443a436eb241367c487274e7197";
        };
    };

    protobuf = pp.buildPythonPackage {
        name = "protobuf";
        propagatedBuildInputs = [ six ];
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/p/protobuf/protobuf-3.0.0b2.tar.gz;
            md5 = "f0d3bd2394345a9af4a277cd0302ae83";
        };
    };

    setproctitle = pp.buildPythonPackage {
        name = "setproctitle";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/s/setproctitle/setproctitle-1.1.9.tar.gz;
            md5 = "95d9e56c69437246460a20804961d70d";
        };
    };

    websockets = pp.buildPythonPackage {
        name = "websockets-3.0";
        src = pkgs.fetchurl {
            url = https://pypi.python.org/packages/source/w/websockets/websockets-3.0.tar.gz;
            md5 = "6575c706f010a5a52a449b3c2dbba84d";
        };
    };
}
