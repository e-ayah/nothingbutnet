import {View, Text} from "react-native";
import type {FeedbackItem} from "../services/types";
import {CHECKPOINT_LABELS} from "../constants/ranges";

type FeedbackItemProps = {
    item: FeedbackItem;
};

const STATUS_TEXT = {
    good: "text-success",
    needs_work: "text-warning",
};

export default function FeedbackItem({item}: FeedbackItemProps) {
    const icon = item.status === "good" ? "✓" : "!";
    const label = CHECKPOINT_LABELS[item.checkpoint];
    return (<View className="flex-row mb-4">
        <View className="w-[24px] items-center mr-2">
            <Text className={`${STATUS_TEXT[item.status]} font-bold text-[19px]`}>{icon}</Text>
        </View>
        <View className="flex-1">
            <Text className="font-semibold text-[23px]">{label}</Text>
            <Text className="text-[19px]">{`${item.angle}°`}</Text>
            <Text className="text-[19px] mt-1">{item.tip}</Text>
        </View>
    </View>
  );
}