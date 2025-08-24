

export interface JobResponse {
    job_id: string;
    status: string;
}

export interface JobStatusResponse {
    status: string;
    story_id?: string;
    error?: string;
}