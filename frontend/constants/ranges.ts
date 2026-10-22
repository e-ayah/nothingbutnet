export const RANGES = {
    elbow_angle: { label: 'Elbow alignment', min: 85, max: 100, checkpoint: 'elbow_alignment' },
    knee_angle: { label: 'Knee bend', min: 150, max: 175, checkpoint: 'knee_bend' },
    shoulder_angle: { label: 'Shoulder position', min: 45, max: 75, checkpoint: 'shoulder_position' },
} as const;
 
export const CHECKPOINT_LABELS: Record<string, string> = {
    elbow_alignment: 'Elbow alignment',
    knee_bend: 'Knee bend',
    shoulder_position: 'Shoulder position',
};
