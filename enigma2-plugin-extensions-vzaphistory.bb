SUMMARY = "Enigma2 plugin to "
DESCRIPTION = "quick zapping between last viewed channels"
HOMEPAGE = "http://gisclub.tv, http://giclub.tv"
SECTION = "base"
PRIORITY = "required"
LICENSE = "PD"
MAINTAINER = "Vasiliks"
LIC_FILES_CHKSUM = "file://README.md;md5=af3dd06a24b0df5271a6a08518c43413"
SRC_URI = "git://github.com/Vasiliks/vZapHistory.git"
S = "${WORKDIR}/git"

inherit gitpkgv
SRCREV = "${AUTOREV}"

VERSION = "0.7" 

PV = "${VERSION}+git${SRCPV}"
PKGV = "${VERSION}+git${GITPKGV}"

inherit allarch distutils-openplugins 

pkg_postinst_${PN} () {
} 
