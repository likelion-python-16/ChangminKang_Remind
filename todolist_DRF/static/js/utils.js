function datetimeToString(datetime){ // datetime을 한국 시간대의 문자열로 변환하는 함수
    if (!datetime) return "-"; // datetime이 없으면 "-"를 반환합니다.
    const date = new Date(datetime); // datetime 문자열을 Date 객체로 변환합니다.
    return date.toLocaleString("ko-KR", { timeZone: "Asia/Seoul" });
}