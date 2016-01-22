{pkgs, stdenv, ksurobot, which}:
stdenv.mkDerivation {
    name = "ksurobot-system";
    src = ./src;
    buildInputs = [which];
    propagatedBuildInputs = [ksurobot];
}
