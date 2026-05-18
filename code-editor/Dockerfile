# hadolint ignore=DL3006
FROM ghcr.io/hassio-addons/debian-base:9.3.0

# Configure locale
ENV \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    PIP_BREAK_SYSTEM_PACKAGES=1

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Copy Python requirements file
COPY requirements.txt /tmp/requirements.txt

# Copy in extensions list
COPY vscode.extensions /root/vscode.extensions

# Patch script that strips legacy-syntax markers from the
# vscode-home-assistant extension's bundled JSON schemas, so YAML
# autocomplete suggests modern keys (`trigger:`, `action:`) instead of
# the deprecated forms (`platform:`, `service:`).
COPY patch-ha-schemas.py /tmp/patch-ha-schemas.py

# Vendored VSIX packages. A file at
# `vendor/${vendor}.${slug}-${version}.vsix` is used in place of the
# VS Code Marketplace download for that extension at build time.
COPY vendor/ /tmp/vendor/

# Setup base system
ARG BUILD_ARCH=amd64
ARG CODE_SERVER_VERSION="v4.118.0"
ARG HA_CLI_VERSION="5.1.0"
# hadolint ignore=SC2181, DL3008
RUN \
    apt-get update \
    \
    && apt-get install -y --no-install-recommends \
        ack=3.8.1-1 \
        build-essential=12.12 \
        colordiff=1.0.21-1 \
        git=1:2.47.3-0+deb13u1 \
        iputils-ping=3:20240905-3 \
        locales=2.41-12+deb13u2 \
        net-tools=2.10-1.3 \
        nginx-light=1.26.3-3+deb13u2 \
        nmap=7.95+dfsg-3 \
        openssh-client=1:10.0p1-7+deb13u2 \
        openssl=3.5.5-1~deb13u2 \
        python3-dev=3.13.5-1 \
        python3-venv=3.13.5-1 \
        python3=3.13.5-1 \
        unzip=6.0-29 \
        uuid-runtime=2.41-5 \
        wget=1.25.0-2 \
        zip=3.0-15 \
        zsh=5.9-8+b21 \
        less=668-1 \
    \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    \
    && curl -fsSL https://bootstrap.pypa.io/get-pip.py | python3 \
    \
    && if [[ "${BUILD_ARCH}" = "aarch64" ]]; then ARCH="arm64"; VSCODE_TARGET="linux-arm64"; fi \
    && if [[ "${BUILD_ARCH}" = "amd64" ]]; then ARCH="amd64"; VSCODE_TARGET="linux-x64"; fi \
    && if [[ -z "${ARCH:-}" || -z "${VSCODE_TARGET:-}" ]]; then echo "Unsupported build architecture: ${BUILD_ARCH}"; exit 1; fi \
    && curl -fJL --retry 5 -o /tmp/code.tar.gz \
        "https://github.com/coder/code-server/releases/download/${CODE_SERVER_VERSION}/code-server-${CODE_SERVER_VERSION#v}-linux-${ARCH}.tar.gz" \
    && mkdir -p /usr/local/lib/code-server \
    && tar zxf \
        /tmp/code.tar.gz \
        --strip 1 -C /usr/local/lib/code-server \
    \
    && ln -s /usr/local/lib/code-server/bin/code-server /usr/local/bin/code-server \
    \
    && mkdir -p /usr/local/share/code-server/vsix \
    && uuid=$(uuidgen) \
    && while read -r ext; do \
        ext="${ext//$'\r'/}"; \
        [[ -z "${ext%%#*}" ]] && continue; \
        extension="${ext%%#*}"; \
        vendor="${extension%%.*}"; \
        slug="${extension#*.}"; \
        version="${ext##*#}"; \
        package_url="https://marketplace.visualstudio.com/_apis/public/gallery/publishers/${vendor}/vsextensions/${slug}/${version}/vspackage"; \
        platform_package_url="${package_url}?targetPlatform=${VSCODE_TARGET}"; \
        \
        echo "Installing vscode extension: ${slug} by ${vendor} @ ${version} for ${VSCODE_TARGET} "; \
        \
        vendored="/tmp/vendor/${extension}-${version}.vsix"; \
        if [[ -f "${vendored}" ]]; then \
            echo "Using vendored VSIX: ${vendored}"; \
            cp "${vendored}" "/usr/local/share/code-server/vsix/${extension}-${version}.vsix"; \
        else \
            echo "${platform_package_url}"; \
            if ! curl -fJL --compressed --retry 5 -o "/usr/local/share/code-server/vsix/${extension}-${version}.vsix" \
                -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36" \
                -H "x-market-user-id: ${uuid}" \
                "${platform_package_url}"; then \
                echo "No ${VSCODE_TARGET} VSIX found for ${extension}; falling back to universal package."; \
                curl -fJL --compressed --retry 5 -o "/usr/local/share/code-server/vsix/${extension}-${version}.vsix" \
                    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36" \
                    -H "x-market-user-id: ${uuid}" \
                    "${package_url}" \
                    || exit 1; \
            fi; \
        fi; \
        vsix_path="/usr/local/share/code-server/vsix/${extension}-${version}.vsix"; \
        unzip -tq "${vsix_path}" >/dev/null \
            || { echo "Downloaded extension package is not a valid VSIX: ${extension} ${version}"; exit 1; }; \
        if [[ "${extension}" = "keesschollaart.vscode-home-assistant" ]]; then \
            echo "Patching ${extension} schemas to remove legacy-syntax markers"; \
            work=$(mktemp -d); \
            unzip -q "${vsix_path}" -d "${work}" \
                || { echo "Failed to unpack VSIX for patching: ${extension}"; rm -rf "${work}"; exit 1; }; \
            python3 /tmp/patch-ha-schemas.py "${work}" \
                || { echo "Schema patch failed: ${extension}"; rm -rf "${work}"; exit 1; }; \
            rm -f "${vsix_path}"; \
            ( cd "${work}" && zip -qr "${vsix_path}" . ) \
                || { echo "Failed to repack VSIX: ${extension}"; rm -rf "${work}"; exit 1; }; \
            unzip -tq "${vsix_path}" >/dev/null \
                || { echo "Repacked VSIX failed validation: ${extension}"; rm -rf "${work}"; exit 1; }; \
            rm -rf "${work}"; \
        fi; \
        sleep 1; \
    done < /root/vscode.extensions \
    && ls -la /usr/local/share/code-server/vsix/ \
    \
    && curl -fsSL --retry 5 -o /usr/bin/ha \
        "https://github.com/home-assistant/cli/releases/download/${HA_CLI_VERSION}/ha_${BUILD_ARCH}" \
    && [[ "$(head -c 4 /usr/bin/ha)" == $'\177ELF' ]] \
    && chmod a+x /usr/bin/ha \
    \
    && git clone --branch master --single-branch --depth 1 \
        "https://github.com/robbyrussell/oh-my-zsh.git" ~/.oh-my-zsh \
    \
    && git clone --branch master --single-branch --depth 1 \
        "https://github.com/zsh-users/zsh-autosuggestions" \
        ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions \
    && git clone --branch master --single-branch --depth 1 \
        "https://github.com/zsh-users/zsh-syntax-highlighting.git" \
        ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting \
    \
    && sed -i -e "s#bin/bash#bin/zsh#" /etc/passwd \
    \
    && update-alternatives \
        --install /usr/bin/python python /usr/bin/python3 10 \
    \
    && pip3 install --no-cache-dir -r /tmp/requirements.txt \
    \
    && apt-get purge -y --auto-remove \
        build-essential \
        python3-dev \
        uuid-runtime \
    \
    && find /usr/local \
        \( \
            \( -type d \( -name test -o -name tests -o -name '__pycache__' \) \) \
            -o \( -type f \( -name '*.pyc' -o -name '*.pyo' \) \) \
        \) \
        -exec rm -rf '{}' + \
    \
    && rm -fr \
        /root/.cache \
        /tmp/* \
        /var/{cache,log}/* \
        /var/lib/apt/lists/*

# Copy root filesystem
COPY rootfs /

RUN \
    chmod a+x /usr/local/bin/code \
    && find /etc/s6-overlay/s6-rc.d \
        \( -name run -o -name finish -o -name up \) \
        -exec chmod a+x '{}' +

# Health check
HEALTHCHECK \
    CMD curl --fail http://127.0.0.1:1338/healthz || exit 1

# Build arguments
ARG BUILD_ARCH
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="Code Editor" \
    io.hass.description="Browser-based code editor for Home Assistant, powered by code-server." \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="app" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.url="https://github.com/gollyjer/home-assistant-code-editor" \
    maintainer="Jeremy Gollehon <jeremy@thegollys.com>" \
    org.opencontainers.image.title="Code Editor" \
    org.opencontainers.image.description="Browser-based code editor for Home Assistant, powered by code-server." \
    org.opencontainers.image.vendor="GollyJer" \
    org.opencontainers.image.authors="Jeremy Gollehon <jeremy@thegollys.com>" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/gollyjer/home-assistant-code-editor" \
    org.opencontainers.image.source="https://github.com/gollyjer/home-assistant-code-editor" \
    org.opencontainers.image.documentation="https://github.com/gollyjer/home-assistant-code-editor/blob/main/code-editor/DOCS.md" \
    org.opencontainers.image.version="${BUILD_VERSION}"
