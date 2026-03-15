import { NextResponse } from "next/server";

export function middleware(request) {
  const host = request.headers.get("x-forwarded-host") || request.headers.get("host") || "";

  if (host === "www.xingjia.xyz") {
    const redirectUrl = request.nextUrl.clone();
    redirectUrl.host = "xingjia.xyz";

    return NextResponse.redirect(redirectUrl, 308);
  }

  const requestHeaders = new Headers(request.headers);
  requestHeaders.set("x-pathname", request.nextUrl.pathname);

  return NextResponse.next({
    request: {
      headers: requestHeaders
    }
  });
}

export const config = {
  matcher: ["/((?!_next|favicon.ico).*)"]
};
