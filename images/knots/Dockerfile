FROM debian:bookworm-slim@sha256:88200866dfff7ea7f5cbcb6ec7c8a701889efe6fe859fe64d6990e4b07ea4171 AS download
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl && rm -rf /var/lib/apt/lists/*
COPY SHA256SUMS /tmp/SHA256SUMS
WORKDIR /tmp
RUN case "$TARGETARCH" in amd64) arch=x86_64;; arm64) arch=aarch64;; *) exit 1;; esac; file="bitcoin-29.4.2.knots20260508-$arch-linux-gnu.tar.gz"; curl --fail --location --retry 3 -o "$file" "https://github.com/bitcoinknots/bitcoin/releases/download/v29.4.2.knots20260508/$file" && grep "  $file$" SHA256SUMS | sha256sum -c - && mkdir /out && tar -xzf "$file" --strip-components=1 -C /out
FROM debian:bookworm-slim@sha256:88200866dfff7ea7f5cbcb6ec7c8a701889efe6fe859fe64d6990e4b07ea4171
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl python3 && rm -rf /var/lib/apt/lists/* && useradd -u 1000 -m bitcoin
COPY --from=download /out/bin/bitcoind /out/bin/bitcoin-cli /usr/local/bin/
COPY entrypoint.py /opt/knots/entrypoint.py
COPY status.py /opt/knots/status.py
COPY LICENSE.bitcoin /usr/share/doc/bitcoin-knots/LICENSE
LABEL org.opencontainers.image.source="https://github.com/connorslab/paperclip-umbrel-app-store" org.opencontainers.image.version="29.4.2.knots20260508"
USER 1000:1000
EXPOSE 8333 8332 8080
ENTRYPOINT ["python3", "/opt/knots/entrypoint.py"]
