{
    mkBasestation,
    python, python35Packages, protobuf, SDL2, lib
}:
let
    pythonPackages = python35Packages;
    mkOpt = lib.optional mkBasestation;
in
let {
    /*body = pythonEnv;*/
    body = pythonPackages.buildPythonPackage rec {
        name = "ksurobot";
        version = "0.1.0";
        src = ../.;

        pythonPath = with pythonPackages; [
            python pythonPackages.protobuf websockets six setproctitle rpigpio ptpython wiringpi
            ] ++ mkOpt [ pysdl2 ];
        buildInputs = [ protobuf ];

        makeWrapperArgs = mkOpt ["--prefix LD_LIBRARY_PATH : ${SDL2}/lib/"];

        configurePhase = ''
            make
        '';
    };
}
