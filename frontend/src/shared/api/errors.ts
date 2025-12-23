export type ApiErrorPayload = {
  code: string;
  message: string;
  details?: unknown;
  request_id?: string;
  timestamp?: string;
};

export class ApiErrorResponse extends Error {
  status: number;
  payload: ApiErrorPayload;

  constructor(status: number, payload: ApiErrorPayload) {
    super(payload.message);
    this.status = status;
    this.payload = payload;
  }
}
