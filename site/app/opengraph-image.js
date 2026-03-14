import { ImageResponse } from "next/og";

export const runtime = "edge";
export const size = {
  width: 1200,
  height: 630
};
export const contentType = "image/png";

export default function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          background:
            "linear-gradient(135deg, #1e3140 0%, #253341 44%, #9a3a1a 100%)",
          color: "#fff8f0",
          fontFamily: "Georgia",
          position: "relative"
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
            background:
              "radial-gradient(circle at 18% 18%, rgba(255,255,255,0.15), transparent 24%), radial-gradient(circle at 85% 20%, rgba(197,79,45,0.35), transparent 24%)"
          }}
        />
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            padding: "70px 74px",
            width: "100%",
            zIndex: 1
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "14px",
              fontSize: 24,
              letterSpacing: "0.08em",
              textTransform: "uppercase"
            }}
          >
            <div
              style={{
                width: 18,
                height: 18,
                borderRadius: 999,
                background: "#f4b59a"
              }}
            />
            My Digital Mentor
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                padding: "10px 16px",
                borderRadius: 999,
                background: "rgba(255,255,255,0.12)",
                color: "#f7d1bf",
                fontSize: 22,
                fontWeight: 700,
                letterSpacing: "0.08em",
                textTransform: "uppercase"
              }}
            >
              Personal AI Writer
            </div>
            <div
              style={{
                display: "flex",
                fontSize: 78,
                lineHeight: 1.04,
                maxWidth: 840,
                letterSpacing: "-0.05em",
                fontWeight: 700
              }}
            >
              Turn your past writing into future writing output.
            </div>
            <div
              style={{
                display: "flex",
                maxWidth: 780,
                color: "rgba(255,248,240,0.8)",
                fontSize: 28,
                lineHeight: 1.5
              }}
            >
              Archive-powered writing for creators, founders, and knowledge workers.
            </div>
          </div>
          <div
            style={{
              display: "flex",
              gap: 20,
              fontSize: 24,
              color: "rgba(255,248,240,0.72)"
            }}
          >
            <div>Retrieve old ideas</div>
            <div>Keep your tone</div>
            <div>Write faster without sounding generic</div>
          </div>
        </div>
      </div>
    ),
    size
  );
}
