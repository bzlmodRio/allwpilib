unix_copts = [
    "-Wno-pedantic",
    "-Wno-format-nonliteral",
    "-Wno-unused-variable",
    "-Wno-unused-function",
    "-Wno-sign-compare",
]

osx_copts = unix_copts

copts = select({
    "@platforms//os:linux": unix_copts + [
        "-Wno-maybe-uninitialized",
    ],
    "@platforms//os:osx": osx_copts,
    "@platforms//os:windows": [
        "/wd4047",
        "/wd4098",
        "/wd4267",
    ],
})

unix_cxxopts = [
    "-Wno-missing-field-initializers",
    "-Wno-pedantic",
    "-fpermissive",
    "-Wno-deprecated-declarations",
    "-Wno-return-type",
    "-Wno-missing-braces",
    "-Wno-null-conversion",
    "-Wno-unused-but-set-variable",
]

osx_cxxopts = unix_cxxopts + [
    "-Wno-unused-variable",
    "-Wno-unused-function",
    "-Wno-sign-compare",
    "-Wno-sometimes-uninitialized",
]

cxxopts = select({
    "@platforms//os:linux": unix_cxxopts + [
        "-Wno-deprecated-enum-enum-conversion",
    ],
    "@platforms//os:osx": osx_cxxopts,
    "@platforms//os:windows": [
        "/wd4068",
        "/wd4101",
        "/wd4200",
        "/wd4576",
        "/wd4715",
    ],
})

mac_linkopts = [
    "-framework",
    "Accelerate",
    "-framework",
    "AVFoundation",
    "-framework",
    "CoreMedia",
]

linkopts = select({
    "@platforms//os:linux": [],
    "@platforms//os:osx": mac_linkopts,
    "@platforms//os:windows": [
        "-DEFAULTLIB:Comdlg32.lib",
        "-DEFAULTLIB:dbghelp.lib",
        "-DEFAULTLIB:Advapi32.lib",
    ],
})
