PKG_CONFIG_PATH=/home/pjreiniger/git/allwpilib/bazel-out/k8-opt/bin/wpiutil/native/wpiutil

cd wpiutil/src/main/python
echo `pwd`
echo $@
../../../../bazel-bin/shared/bazel/rules/robotpy/semiwrap create-yaml --write