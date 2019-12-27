# Git



> Git은 분산 버전 관리시스템(DVCS)이다.
>
> 소스코드의 버전 및 이력을 관리 할 수 있다.



# 준비하기



> 윈도우에서 git을 활용하기 위해 [git bash](https://gitforwindows.org/)를 설치한다.
>
> git을 활용하기 위해서 GUI 툴인 `source tree`,`github`,`desktop`등을 활용 할 수도 있다. 
>
> 초기 설치를 완료한 이후에 컴퓨터에 `author` 정보를 입력한다. 이메일 정보를  github에 가입된 이메일로 일치시켜야 commit 이력들이 관리된다.
>
> ```bash
> $ git config --global user.name headbreakz
> $ git config --global user.email 1005night@naver.com
> ```



> 현재 등록된 정보 확인하기
>
> ```bash
> $ git config user.name
> $ git config user.email
> ```
>
> 

## 로컬저장소 (repository) 활용하기



### 1.저장소 초기화

```bash
$ git init
Initialized empty Git repository in C:/Users/student/Desktop/til/.git/
```

* `.git` 폴더가 생성되며, 여기에 git과 관련된 모든 정보가 저장된다.
* git bash에 `(master)`라고 표현되는데 이는 `master` 브랜치에 있다는 뜻이다.



### 2.add

`working directory`, 즉 작업공간에서 변경된 사항을 이력으로 저장하기 위해서는 반드시 `staging area`를 거쳐야 한다.

```bash
$ git add markdown.md #특정 파일
$ git add images/ #특정 폴더
$ git add . # 현재 디렉토리
```

* `add` 전 상태

  ```bash
  $ git status
  On branch master
  
  No commits yet
  
  # 트래킹 되고 있지 않은 파일들
  # => commit 이력에 한번도 담기지 않은 파일들
  Untracked files:
  # commit 준비에 포함시킬려면 add 명령어를 사용함
    (use "git add <file>..." to include in what will be committed)
          git.md
          images/
          markdown.md
  #아직 commit 준비된 것은 없지만, untracked files은 존재함
  nothing added to commit but untracked files present (use "git add" to track)
  ```

* `add` 후 상태

  ```bash
  $ git status
  On branch master
  
  No commits yet
  
  #commit 변화 =>staging area에 있는 파일들
  Changes to be committed:
    (use "git rm --cached <file>..." to unstage)
          new file:   images/images.jpg
  
  Untracked files:
    (use "git add <file>..." to include in what will be committed)
          git.md
          markdown.md
  ```

### 3. `commit`

commit은 이력을 확정짓는 명령어로, 해당 시점의 스냅샷을 기록한다. 

commit 시에는 반드시 메세지를 작성 해야하며, 메세지는 변경사항을 알 수 있도록 명확하게 작성한다.

```bash
$ git commit -m '마크다운 및 정리'
[master (root-commit) 20feb8a] 마크다운 및 정리
 3 files changed, 80 insertions(+)
 create mode 100644 git.md
 create mode 100644 images/images.jpg
 create mode 100644 markdown.md
```

commit 이후에는 아래의 명령어를 통해 지금까지 작성된 이력을 확인한다.

```bash
$ git log
commit 20feb8ae2c6b721e3f84126a6648bf0dfb01f890 (HEAD -> master)
Author: headbreakz <1005night@naver.com>
Date:   Thu Dec 26 14:35:34 2019 +0900

    마크다운 및 정리

$ git log --oneline
20feb8a (HEAD -> master) 마크다운 및 정리

$ git log -1
commit 20feb8ae2c6b721e3f84126a6648bf0dfb01f890 (HEAD -> master)
Author: headbreakz <1005night@naver.com>
Date:   Thu Dec 26 14:35:34 2019 +0900

    마크다운 및 정리

```



commit hashcode를 바탕으로 구분된다. 



## 원격저장소(remote repository) 활용하기

원격 저장소 기능을 제공하는 다양한 서비스 중에 github을 기준으로 설명한다.



### 0.준비사항

* Github에 repository 생성



### 1.원격 저장소 등록

```bash
$ git remote add origin Githuburl
```

* 원격저장소(remote)로 `origin`이라는 이름으로 `github url`을 등록(`add`)한다

* 등록된 원격 저장소 목록을 보기 위해서는 아래의 명령어를 활용한다.

  ```bash
  $ git remote -v
  origin  https://github.com/Headbreakz/til.git (fetch)
  origin  https://github.com/Headbreakz/til.git (push)
  ```

### 2.push - 원격저장소 업로드

```bash
$ git push origin master
```

`origin`으로 설정된 원격 저장소에 `master`브랜치로 업로드(`push`)

이후 변경사항이 생길 때마다,` add`-`commit`,`push` 를 반복하면 된다.

그리고, 항상 모든 명령어 이후에 연관된 상태를 확인하자.

`status`,`log`,`remote -v`



### 3.pull

```bash
$ git pull origin master
```

원격 저장소의 변경 사항을 받아온다.



### 4.`clone`

```bash
$ git clone github url
```

원격 저장소를 복제 한다.

**주의 ! `init` 명령어와 같이 기억하자**



# git logout방법

윈도우 검색 - `자격`-`자격 증명 관리자`-`github`-`제거`

