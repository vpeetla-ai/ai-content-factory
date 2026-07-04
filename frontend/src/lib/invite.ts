const INVITE_KEY = "acf_invite_code";

export function setInviteCode(code: string) {
  if (typeof window !== "undefined") sessionStorage.setItem(INVITE_KEY, code);
}

export function getInviteCode(): string | null {
  if (typeof window === "undefined") return null;
  return sessionStorage.getItem(INVITE_KEY);
}

export function clearInviteCode() {
  if (typeof window !== "undefined") sessionStorage.removeItem(INVITE_KEY);
}
