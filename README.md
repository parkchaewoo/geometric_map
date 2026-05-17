# 3D 해발 고도 지도

대륙·국가·도시를 골라 실제 해발 고도를 회전 가능한 3D 서피스 그래프로 보는 앱.
DEM 데이터는 AWS Open Data "Terrarium" 타일을 사용하며, 타일 다운로드와
고도 디코딩이 모두 클라이언트(브라우저/WebView)에서 일어납니다. 별도 백엔드
서버가 필요 없습니다.

## 구조

```
web/                     단일 코드베이스 (데스크톱·안드로이드 공용)
  index.html  app.js     UI
  geo.js                 고도 엔진: 타일 fetch + 디코딩 + 그리드 생성
  regions.json           대륙/국가/도시 데이터 (regions.py에서 생성)
  plotly.min.js          Plotly 오프라인 번들
regions.py               지역 데이터 원본 (단일 소스)
gen_regions.py           regions.py -> web/regions.json 생성
app.py                   데스크톱 개발용 정적 서버 (선택)
android/                 안드로이드 WebView 래퍼 (Gradle 프로젝트)
```

지역을 수정하려면 `regions.py`를 고치고 `python3 gen_regions.py` 실행.

## 데스크톱에서 실행

```
pip install -r requirements.txt
python3 app.py            # http://localhost:5050  (PORT 로 변경 가능)
```

`app.py`는 정적 서버일 뿐이며 모든 처리는 브라우저에서 수행됩니다.

## 안드로이드 빌드

`web/`은 빌드 시 `android/app/src/main/assets/web/`로 자동 복사됩니다
(`syncWebAssets` Gradle 태스크). `web/plotly.min.js`는 저장소에 포함되어
있으므로 안드로이드 빌드에 파이썬이 필요 없습니다.

1. **Android Studio**로 `android/` 폴더 열기 (Gradle 래퍼 jar이 없으면
   Android Studio가 자동 생성). 또는 Gradle 설치 후 `android/`에서
   `gradle wrapper` 실행 후 아래 명령 사용.
2. 디버그 APK:
   ```
   cd android && ./gradlew assembleDebug
   # 산출물: app/build/outputs/apk/debug/app-debug.apk
   ```

## Google Play 출시

1. **업로드 키스토어 생성** (최초 1회):
   ```
   keytool -genkey -v -keystore release.jks -keyalg RSA -keysize 2048 \
     -validity 10000 -alias upload
   ```
2. `android/keystore.properties` 작성 (gitignore 처리됨):
   ```
   storeFile=/절대/경로/release.jks
   storePassword=********
   keyAlias=upload
   keyPassword=********
   ```
3. 출시용 **AAB** 빌드:
   ```
   cd android && ./gradlew bundleRelease
   # 산출물: app/build/outputs/bundle/release/app-release.aab
   ```
4. Google Play Console에서 앱 생성 → 프로덕션 트랙에 `app-release.aab`
   업로드. Play 앱 서명 사용 시 위 키는 업로드 키로 등록됩니다.
5. 버전을 올릴 때마다 `android/app/build.gradle`의 `versionCode`(정수
   증가)와 `versionName`을 수정.

### 출시 전 체크리스트

- `applicationId` (현재 `com.geomap.elevation`) 를 본인 도메인 기준으로
  변경할지 결정 — 한 번 출시하면 변경 불가.
- 앱 아이콘(`res/drawable/ic_launcher_foreground.xml`)·이름
  (`res/values/strings.xml`) 최종 확인.
- Play Console 요구 자료: 스크린샷, 개인정보처리방침 URL(인터넷 권한만
  사용, 위치/개인정보 미수집), 콘텐츠 등급 설문.
- 출시 연도 정책에 따라 `targetSdk` 상향이 필요할 수 있음(현재 34).

## 비고

- 인터넷 권한만 사용 (DEM 타일 다운로드용). 위치·계정 등 민감 권한 없음.
- 타일 서버 CORS가 개방되어 있어 WebView에서 직접 픽셀 디코딩이 가능.
- 이 환경에서는 Android SDK/Gradle을 실행할 수 없어 APK 빌드·서명·기기
  테스트는 검증하지 못했습니다. 코드 구조와 웹 앱 로직(타일 수학은
  파이썬 구현과 수치 일치 확인)은 검증되었습니다.
