const axiosInstance = axios.create({ // axios 인스턴스를 생성합니다. 나중에 API 호출에 사용할 것입니다.
    baseURL: "/todo/", // API의 기본 URL을 설정합니다. 이 URL은 나중에 API 호출 시 사용됩니다. 즉 todo/list인데 todo/todo/list 이런 오류를 방지해주기 위한 초기화
    headers : {
      "X-CSRFToken": getCookie("csrftoken"), // CSRF 토큰을 가져옵니다. Django에서 CSRF 보호를 위해 필요합니다.
      // "content-type":"application/json" // 요청의 콘텐츠 유형을 JSON으로 설정합니다.
      "Content-Type":"multipart/form-data" // 요청의 콘텐츠 유형을 multipart/form-data로 설정합니다. 파일 업로드를 지원하기 위해 필요합니다. (예: 이미지 업로드 )
    }
});

window.axiosInstance = axiosInstance; // 전역 객체에 axios 인스턴스를 할당합니다. 이렇게 하면 다른 스크립트에서도 이 인스턴스를 사용할 수 있습니다.