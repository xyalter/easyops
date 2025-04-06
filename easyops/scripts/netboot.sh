#!/usr/bin/env bash
# created by xxy1991

BOOT_PATH='/boot/new'

BASE_URI='main/installer-amd64/current/images/netboot'
BASE_URI2='main/installer-amd64/current/legacy-images/netboot'
NETBOOTFILE='netboot.tar.gz'

GRUB40='/etc/grub.d/40_custom'
DGRUB='/etc/default/grub'

# netboot_download(str mirror, str os, str ver_code)
netboot_download() {
    rm -rf "${BOOT_PATH:?}/"*
    if [ ! -d ${BOOT_PATH} ]; then mkdir ${BOOT_PATH}; fi
    cd "${BOOT_PATH}" || exit

    if [ "${3}" = "focal" ]; then
        wget -Nq "${1}/${2}/dists/${3}/${BASE_URI2}/${NETBOOTFILE}" &&
            tar -zxf "${NETBOOTFILE}"
    else
        wget -Nq "${1}/${2}/dists/${3}/${BASE_URI}/${NETBOOTFILE}" &&
            tar -zxf "${NETBOOTFILE}"
    fi
}

# netboot_grub(str cfg_path)
netboot_grub() {
    grep 'New Install' "${GRUB40}" >&/dev/null
    if [ $? -eq 1 ]; then
        cat "$1" >>"${GRUB40}"
    fi
    sed -i '/^GRUB_DEFAULT=/c\GRUB_DEFAULT="New Install"' "${DGRUB}"
    sed -i '/^GRUB_TIMEOUT=/c\GRUB_TIMEOUT=1' "${DGRUB}"
    sed -i '/^GRUB_HIDDEN_TIMEOUT=/d' "${DGRUB}"
    update-grub
}

# netboot_preseed(str os, str cfg_path)
netboot_preseed() {
    cd "${BOOT_PATH}" || exit
    cp "$2" ./preseed.cfg
    initrd_file="${1}-installer/amd64/initrd"
    gunzip "${initrd_file}.gz"
    echo preseed.cfg | cpio -H newc -o -A -F "${initrd_file}"
    gzip "${initrd_file}"
}

# netboot_attach(str os, str src_path, str dest_path, str base_path)
netboot_attach() {
    cd "${BOOT_PATH}" || exit
    initrd_file="${1}-installer/amd64/initrd"
    attach_file="${2}"
    dest_path="${3}"
    base_path="${4}"
    gunzip "${initrd_file}.gz"
    if [ -f "${base_path}/${attach_file}" ]; then
        cd "${base_path}" || exit
        find . -maxdepth 1 -name "${attach_file}" -print0 |
            cpio --null -H newc -o -A -F "${BOOT_PATH}/${initrd_file}"
        # find . -maxdepth 1 -name "${attach_file}" -print0 | \
        #     cpio --null -H newc -o -F "/tmp/append.cpio"
        cd "${BOOT_PATH}" || exit
    elif [ -d "${base_path}/${attach_file}" ]; then
        mkdir -p "/tmp/easyops/${dest_path}"
        find "/tmp/easyops" -mindepth 1 -print0 | \
            pax -w -0 -a -f "${BOOT_PATH}/${initrd_file}" \
                -x sv4cpio -s "|^/tmp/easyops/||"

        # find "${attach_file}" -print0 |
        #   cpio --null -H newc -ov -A -F "${BOOT_PATH}/${initrd_file}"
        # find "${attach_file}" -depth -print0 | cpio --null -H newc -o -F "/tmp/append.cpio"
        # cpio -tv < "/tmp/append.cpio"

        # cp -p "${BOOT_PATH}/${initrd_file}" "/tmp/append.cpio"
        pax -w -a -f "${BOOT_PATH}/${initrd_file}" \
            -x sv4cpio -s "|^${base_path}|${dest_path}|" \
            "${base_path}/${attach_file}"
    else
        echo "attach file exception: ${base_path}/${attach_file}"
    fi
    #    gzip "/tmp/append.cpio"
    #    cp -p "${BOOT_PATH}/${initrd_file}.gz" "${BOOT_PATH}/${initrd_file}.gz.ori"
    #    cat "${BOOT_PATH}/${initrd_file}.gz.ori" "/tmp/append.cpio.gz" >"${BOOT_PATH}/${initrd_file}.gz"
    #    rm -f "${BOOT_PATH}/${initrd_file}.gz.ori"
    #    rm -f "/tmp/append.cpio.gz"
    gzip "${initrd_file}"
}

"$@"
