FROM debian:bookworm-slim@sha256:88200866dfff7ea7f5cbcb6ec7c8a701889efe6fe859fe64d6990e4b07ea4171 AS build
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates git build-essential cmake pkgconf libcurl4-openssl-dev libjansson-dev libsodium-dev libmicrohttpd-dev python3 && rm -rf /var/lib/apt/lists/*
ARG CONVOY_COMMIT=ac9b70c8b361f14e90e2c963b429a9bbb414aecb
RUN git clone https://github.com/CONVOYMining/datum_gateway.git /src && cd /src && git checkout "$CONVOY_COMMIT" && git merge-base --is-ancestor 56c31f4 HEAD && test "$(git rev-parse HEAD)" = "$CONVOY_COMMIT"
COPY brand.py icon.svg /branding/
RUN python3 /branding/brand.py
RUN cmake -S /src -B /build -DCMAKE_BUILD_TYPE=Release && cmake --build /build -j2 && /build/datum_gateway --test
FROM debian:bookworm-slim@sha256:88200866dfff7ea7f5cbcb6ec7c8a701889efe6fe859fe64d6990e4b07ea4171
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates libcurl4 libjansson4 libsodium23 libmicrohttpd12 python3 && rm -rf /var/lib/apt/lists/* && useradd -u 1000 -m gateway
COPY --from=build /build/datum_gateway /usr/local/bin/datum_gateway
COPY --from=build /src/LICENSE /usr/share/doc/convoy/LICENSE
COPY runtime/ /opt/convoy/
LABEL org.opencontainers.image.source="https://github.com/connorslab/paperclip-umbrel-app-store" org.opencontainers.image.revision="ac9b70c8b361f14e90e2c963b429a9bbb414aecb"
USER 1000:1000
WORKDIR /data
EXPOSE 7152 23334
ENTRYPOINT ["python3", "/opt/convoy/entrypoint.py"]
