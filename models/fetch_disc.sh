#!/bin/bash
NUM=$1
OUT=$2
CURSOR="null"
: > $OUT
gh api graphql -f query="
query {
  repository(owner: \"ggml-org\", name: \"llama.cpp\") {
    discussion(number: $NUM) { title createdAt body }
  }
}" --jq '.data.repository.discussion | "TITLE: \(.title)\nCREATED: \(.createdAt)\n---BODY---\n\(.body)"' >> $OUT
for i in $(seq 1 30); do
  RES=$(gh api graphql -f query="
  query {
    repository(owner: \"ggml-org\", name: \"llama.cpp\") {
      discussion(number: $NUM) {
        comments(first: 50, after: $CURSOR) {
          pageInfo { hasNextPage endCursor }
          nodes { author { login } createdAt body replies(first: 30) { nodes { author { login } createdAt body } } }
        }
      }
    }
  }")
  echo "$RES" | jq -r '.data.repository.discussion.comments.nodes[] | "\n===COMMENT by \(.author.login // "?") at \(.createdAt)===\n\(.body)\n\(.replies.nodes[]? | "\n--REPLY by \(.author.login // "?") at \(.createdAt)--\n\(.body)")"' >> $OUT
  HAS=$(echo "$RES" | jq -r '.data.repository.discussion.comments.pageInfo.hasNextPage')
  END=$(echo "$RES" | jq -r '.data.repository.discussion.comments.pageInfo.endCursor')
  if [ "$HAS" != "true" ]; then break; fi
  CURSOR="\"$END\""
done
wc -l $OUT
