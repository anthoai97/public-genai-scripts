SELECT 
  j.jobid,
  j.jobname,
  COALESCE(
    CASE 
      WHEN r.status = 'succeeded' THEN 1
      WHEN r.status = 'failed' THEN -1
      ELSE 0
    END, 0
  ) AS job_status
FROM cron.job j
LEFT JOIN LATERAL (
  SELECT status
  FROM cron.job_run_details r
  WHERE r.jobid = j.jobid
  ORDER BY end_time DESC
  LIMIT 1
) r ON true;
