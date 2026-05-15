CREATE TABLE IF NOT EXISTS meetings (
  meeting_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  customer_name TEXT,
  permission_flag BOOLEAN NOT NULL,
  recording_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS transcript_segments (
  meeting_id TEXT NOT NULL REFERENCES meetings(meeting_id) ON DELETE CASCADE,
  segment_id TEXT NOT NULL,
  start_time TEXT NOT NULL,
  end_time TEXT NOT NULL,
  speaker_label TEXT NOT NULL,
  speaker_name TEXT,
  speaker_org TEXT NOT NULL CHECK (speaker_org IN ('customer', 'nutanix', 'partner', 'unknown')),
  speaker_confidence TEXT CHECK (speaker_confidence IN ('high', 'medium', 'low', 'unknown')),
  raw_text TEXT NOT NULL,
  normalized_text TEXT NOT NULL,
  asr_confidence DOUBLE PRECISION,
  diarization_confidence DOUBLE PRECISION,
  overlap BOOLEAN NOT NULL DEFAULT false,
  technical_terms_detected JSONB NOT NULL DEFAULT '[]'::jsonb,
  correction_notes JSONB NOT NULL DEFAULT '[]'::jsonb,
  source_asr TEXT NOT NULL,
  source_diarization TEXT NOT NULL,
  recording_hash TEXT NOT NULL,
  PRIMARY KEY (meeting_id, segment_id)
);

CREATE TABLE IF NOT EXISTS evidence_items (
  evidence_id TEXT PRIMARY KEY,
  meeting_id TEXT NOT NULL REFERENCES meetings(meeting_id) ON DELETE CASCADE,
  chunk_id TEXT NOT NULL,
  item_type TEXT NOT NULL,
  domain TEXT NOT NULL,
  statement TEXT NOT NULL,
  explicitness TEXT NOT NULL,
  speaker JSONB NOT NULL,
  speaker_org TEXT NOT NULL CHECK (speaker_org IN ('customer', 'nutanix', 'partner', 'unknown')),
  segment_ids JSONB NOT NULL,
  timestamp_start TEXT NOT NULL,
  timestamp_end TEXT NOT NULL,
  evidence_quote TEXT NOT NULL,
  quote_match_status TEXT NOT NULL CHECK (quote_match_status IN ('exact_match', 'normalized_match', 'unverified')),
  normalized_terms JSONB NOT NULL DEFAULT '[]'::jsonb,
  related_evidence_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  requires_human_review BOOLEAN NOT NULL DEFAULT false,
  review_reason TEXT,
  source_stage TEXT,
  source_evidence_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
  extraction_model TEXT NOT NULL,
  prompt_version TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS report_sections (
  meeting_id TEXT NOT NULL REFERENCES meetings(meeting_id) ON DELETE CASCADE,
  section_id TEXT NOT NULL,
  section_title TEXT NOT NULL,
  draft_markdown TEXT NOT NULL,
  claims JSONB NOT NULL,
  builder_model TEXT NOT NULL,
  prompt_version TEXT NOT NULL,
  status TEXT NOT NULL,
  PRIMARY KEY (meeting_id, section_id)
);

CREATE TABLE IF NOT EXISTS validation_results (
  meeting_id TEXT NOT NULL REFERENCES meetings(meeting_id) ON DELETE CASCADE,
  section_id TEXT NOT NULL,
  validator_model TEXT NOT NULL,
  prompt_version TEXT NOT NULL,
  overall_status TEXT NOT NULL,
  findings JSONB NOT NULL,
  coverage JSONB NOT NULL,
  claim_audit JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (meeting_id, section_id, validator_model, created_at)
);

CREATE INDEX IF NOT EXISTS idx_transcript_segments_meeting_time ON transcript_segments(meeting_id, start_time);
CREATE INDEX IF NOT EXISTS idx_evidence_items_meeting_domain ON evidence_items(meeting_id, domain);
CREATE INDEX IF NOT EXISTS idx_evidence_items_type ON evidence_items(item_type);
CREATE INDEX IF NOT EXISTS idx_evidence_items_review ON evidence_items(meeting_id, requires_human_review);
