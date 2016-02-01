{python, python35Packages, protobuf, SDL2}:
let
    pythonPackages = python35Packages;
in
let {
    /*body = pythonEnv;*/
    body = pythonPackages.buildPythonPackage rec {
        name = "ksurobot";
        version = "0.1.0";
        src = ../.;

        pythonPath = with pythonPackages; [
            python pythonPackages.protobuf websockets six setproctitle rpigpio ptpython wiringpi
            pysdl2
        ];
        buildInputs = [ protobuf ];

        makeWrapperArgs = ["--prefix LD_LIBRARY_PATH : ${SDL2}/lib/"];

        configurePhase = ''
            make
        '';
    };
}
