{python, python35Packages, protobuf}:
let
    pythonPackages = python35Packages;
in
let {
    /*body = pythonEnv;*/
    body = pythonPackages.buildPythonPackage rec {
        name = "ksurobot";
        version = "0.1.0";
        src = ../.;

        pythonPath = with pythonPackages; [ python pythonPackages.protobuf websockets six setproctitle rpigpio ptpython wiringpi ];
        /*propagatedBuildInputs = [python];*/
        buildInputs = [ protobuf ];

        configurePhase = ''
            make
        '';
    };
}
