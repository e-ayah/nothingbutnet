// Sixers#02: 10th–90th percentile of angles at hand-marked release frames
// on 20 made shots (n = 14 elbow, 15 knee, 16 shoulder), rounded to 5°.
export const RANGES = {
    elbow_angle: { label: 'Elbow alignment', min: 115, max: 165, checkpoint: 'elbow_alignment' },
    knee_angle: { label: 'Knee bend', min: 140, max: 170, checkpoint: 'knee_bend' },
    shoulder_angle: { label: 'Shoulder position', min: 10, max: 150, checkpoint: 'shoulder_position' },
} as const;
 
export const CHECKPOINT_LABELS: Record<string, string> = {
    elbow_alignment: 'Elbow alignment',
    knee_bend: 'Knee bend',
    shoulder_position: 'Shoulder position',
};
