import {View, Text} from "react-native";

type AngleCardProps = {
    name: string;
    value: number | null;
    min: number;
    max: number;
    status: "good" | "needs_work";
};

const STATUS_BG = {
    good: "bg-success",
    needs_work: "bg-warning",
};

export default function AngleCard({name, value, min, max, status}: AngleCardProps) {
    const measured = value !== null;
    return (<View className={`${STATUS_BG[status]} max-w-[360px] p-4 mb-4 rounded-[15px]`}>
        <Text className="text-white text-center font-semibold text-[23px]">{name}</Text>
        <Text className="text-white text-center font-bold text-[45px]">{measured ? `${value}°` : "—"}</Text>
        {measured ? (<Text className="text-white text-center text-[19px]">{`Optimal ${min}–${max}°`}</Text>) : (<Text className="text-white text-center text-[19px]">Couldn't measure</Text>)}
    </View>
  );
}