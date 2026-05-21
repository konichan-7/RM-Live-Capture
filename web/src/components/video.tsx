import { useEffect, useRef } from "react";
import { Modal } from "antd";

import Hls from "hls.js";

export default function Video({ src = "", className = '', ...props }) {
    const videoRef = useRef<HTMLVideoElement>(null);

    useEffect(() => {
        if (!src || src === '/api/video/file/' || !src.includes('/api/video/file/')) {
            return;
        }
        if (!Hls.isSupported()) {
            return;
        }
        const hls = new Hls();
        hls.loadSource(src);
        hls.attachMedia(videoRef.current!);
        hls.on(Hls.Events.ERROR, (err, data) => {
            if (data.fatal) {
                try {
                    if (data.networkDetails.response) {
                        const error = JSON.parse(data.networkDetails.response);
                        Modal.error({
                            title: 'Error',
                            content: error.msg,
                        });
                    }
                } catch (_) {
                    Modal.error({
                        title: 'Error',
                        content: data.error.message,
                    });
                }

                hls.destroy();
            }
        });
        return () => hls.destroy();
    }, [src])

    return (
        <video
            ref={videoRef}
            controls
            {...props}
            src={src}
            className={className}
        />
    )
}
