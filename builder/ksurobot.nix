{python, python35Packages}:
let
    pythonPackages = python35Packages;
in
let {
    body = pythonPackages.buildPythonPackage rec {
        name = "ksurobot";
        version = "0.1.0";
        src = ../.;

        pythonPath = with pythonPackages; [ python websockets six setproctitle rpigpio ptpython ];
        propagatedBuildInputs = [python pythonPackages.wrapPython];

        configurePhase = ''
            make
        '';

        /*makeFlagsArray=[ "PREFIX=\${out}" ];*/

        /*propagatedBuildInputs = */
    };
}
