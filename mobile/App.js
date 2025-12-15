import React, { useEffect, useState } from "react";
import { I18nManager, SafeAreaView, StyleSheet, Text, View, FlatList, TouchableOpacity, Linking } from "react-native";
import Constants from "expo-constants";
import { ApiClient } from "@menna/shared";

export default function App() {
  const [providers, setProviders] = useState([]);
  const [direction, setDirection] = useState("rtl");
  const client = new ApiClient(Constants.expoConfig?.extra?.apiBase || process.env.API_BASE_URL || "http://localhost:8000");

  useEffect(() => {
    I18nManager.forceRTL(direction === "rtl");
    client
      .listProviders()
      .then(setProviders)
      .catch(() =>
        setProviders([
          {
            id: 1,
            name: "منى – سباكة",
            bio_i18n: { ar: "سريعة الاستجابة في حيفا", he: "", en: "" },
            verified: true,
            languages: ["ar", "he"],
            categories: [2],
            city_id: 2,
            area_ids: [3],
            pricing_hint: "زيارة 150 ₪",
            availability: "اليوم",
            whatsapp: "+972501234567",
            phone: "+972501234567",
            rating: 4.8,
            rating_count: 44
          }
        ])
      );
  }, [direction]);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>منّا | Menna</Text>
        <TouchableOpacity onPress={() => setDirection(direction === "rtl" ? "ltr" : "rtl")}>
          <Text style={styles.link}>{direction === "rtl" ? "EN" : "عربي"}</Text>
        </TouchableOpacity>
      </View>
      <FlatList
        data={providers}
        keyExtractor={(item) => item.id?.toString() || Math.random().toString()}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <View style={styles.row}>
              <Text style={styles.name}>{item.name}</Text>
              {item.verified && <Text style={styles.badge}>موثوق</Text>}
            </View>
            <Text style={styles.muted}>{item.bio_i18n["ar"] || item.bio_i18n["en"]}</Text>
            <Text style={styles.muted}>اللغات: {item.languages.join(", ")}</Text>
            <View style={styles.row}>
              <TouchableOpacity style={styles.button} onPress={() => Linking.openURL(`https://wa.me/${item.whatsapp}`)}>
                <Text style={styles.buttonText}>واتساب</Text>
              </TouchableOpacity>
              <TouchableOpacity style={[styles.button, styles.callButton]} onPress={() => Linking.openURL(`tel:${item.phone}`)}>
                <Text style={styles.buttonText}>اتصال</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f3efe8",
    padding: 16
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12
  },
  title: {
    fontSize: 22,
    fontWeight: "800"
  },
  link: {
    color: "#f28705",
    fontWeight: "700"
  },
  card: {
    backgroundColor: "#fff",
    padding: 16,
    borderRadius: 14,
    marginBottom: 12,
    shadowColor: "#000",
    shadowOpacity: 0.08,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 4 },
    elevation: 2
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between"
  },
  name: {
    fontSize: 18,
    fontWeight: "700"
  },
  badge: {
    backgroundColor: "#0ea5e9",
    color: "#fff",
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 12,
    fontSize: 12
  },
  muted: {
    color: "#475569",
    marginTop: 6,
    marginBottom: 4
  },
  button: {
    backgroundColor: "#0f172a",
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderRadius: 12,
    marginTop: 8
  },
  callButton: {
    backgroundColor: "#f28705"
  },
  buttonText: {
    color: "#fff",
    fontWeight: "700"
  }
});
